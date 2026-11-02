/**
 * Starfall Breakout - Vercel Serverless Function: Global Leaderboard
 * Supports Supabase REST API (PostgREST) and Vercel KV / Upstash Redis.
 * Pure native fetch, zero npm dependencies.
 */

module.exports = async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Database credentials (Supabase or Redis)
  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

  const REDIS_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const REDIS_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  const LEADERBOARD_KEY = 'starfall_global_leaderboard';

  // Fallback demo rankings if no online DB is connected yet
  const mockLeaderboard = [
    { rank: 1, name: 'STELLA-01', score: 32500, time: 210, formattedTime: '03:30', diff: 'hardcorez' },
    { rank: 2, name: 'CYBER-ACE', score: 24200, time: 165, formattedTime: '02:45', diff: 'hard' },
    { rank: 3, name: 'NOVA-STAR', score: 17800, time: 130, formattedTime: '02:10', diff: 'hardcorez' },
    { rank: 4, name: 'TITAN-SLAY', score: 12500, time: 95, formattedTime: '01:35', diff: 'normal' },
    { rank: 5, name: 'VOID-FOX', score: 8600, time: 72, formattedTime: '01:12', diff: 'normal' },
    { rank: 6, name: 'ARCADE-X', score: 6200, time: 54, formattedTime: '00:54', diff: 'easy' },
    { rank: 7, name: 'RETRO-99', score: 4500, time: 40, formattedTime: '00:40', diff: 'easy' }
  ];

  // --- GET: Retrieve Top 10 High Scores ---
  if (req.method === 'GET') {
    // 1. Priority: Supabase REST API
    if (SUPABASE_URL && SUPABASE_KEY) {
      try {
        const cleanUrl = SUPABASE_URL.replace(/\/+$/, '');
        const endpoint = `${cleanUrl}/rest/v1/leaderboard?select=name,score,time,formatted_time,diff,created_at&order=score.desc&limit=10`;
        const response = await fetch(endpoint, {
          headers: {
            apikey: SUPABASE_KEY,
            Authorization: `Bearer ${SUPABASE_KEY}`
          }
        });

        if (!response.ok) {
          throw new Error(`Supabase response status: ${response.status}`);
        }

        const rows = await response.json();
        const leaderboard = (Array.isArray(rows) ? rows : []).map((row, index) => ({
          rank: index + 1,
          name: String(row.name || 'PILOT').slice(0, 10),
          score: Number(row.score) || 0,
          time: Number(row.time) || 0,
          formattedTime: String(row.formatted_time || row.formattedTime || '00:00'),
          diff: String(row.diff || 'normal')
        }));

        return res.status(200).json({
          status: 'live_supabase',
          leaderboard: leaderboard.length > 0 ? leaderboard : mockLeaderboard
        });
      } catch (err) {
        console.error('Supabase fetch error:', err);
        return res.status(200).json({
          status: 'fallback',
          message: 'Gagal mengambil data dari Supabase, menampilkan ranking demo.',
          leaderboard: mockLeaderboard
        });
      }
    }

    // 2. Secondary: Upstash / Vercel KV Redis
    if (REDIS_URL && REDIS_TOKEN) {
      try {
        const response = await fetch(`${REDIS_URL}/zrevrange/${LEADERBOARD_KEY}/0/9`, {
          headers: { Authorization: `Bearer ${REDIS_TOKEN}` }
        });

        if (!response.ok) {
          throw new Error(`Upstash response status: ${response.status}`);
        }

        const data = await response.json();
        const rawEntries = Array.isArray(data.result) ? data.result : [];

        const leaderboard = rawEntries.map((raw, index) => {
          try {
            const item = typeof raw === 'string' ? JSON.parse(raw) : raw;
            return {
              rank: index + 1,
              name: String(item.name || 'PILOT').slice(0, 10),
              score: Number(item.score) || 0,
              time: Number(item.time) || 0,
              formattedTime: String(item.formattedTime || '00:00'),
              diff: String(item.diff || 'normal')
            };
          } catch {
            return {
              rank: index + 1,
              name: 'PILOT',
              score: 0,
              time: 0,
              formattedTime: '00:00',
              diff: 'normal'
            };
          }
        });

        return res.status(200).json({
          status: 'live_redis',
          leaderboard: leaderboard.length > 0 ? leaderboard : mockLeaderboard
        });
      } catch (err) {
        console.error('Redis fetch error:', err);
        return res.status(200).json({
          status: 'fallback',
          message: 'Gagal mengambil data dari Redis, menampilkan ranking demo.',
          leaderboard: mockLeaderboard
        });
      }
    }

    // 3. Fallback: Demo Mode
    return res.status(200).json({
      status: 'demo',
      message: 'Database belum terhubung. Menampilkan data ranking demo.',
      leaderboard: mockLeaderboard
    });
  }

  // --- POST: Submit a New High Score ---
  if (req.method === 'POST') {
    try {
      const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
      let rawName = String(body.name || '').trim().toUpperCase();
      const score = Math.floor(Number(body.score) || 0);
      const time = Math.floor(Number(body.time) || 0);
      const diff = ['easy', 'normal', 'hard', 'hardcorez'].includes(body.diff) ? body.diff : 'normal';

      // Validate name (2 - 10 alphanumeric characters / hyphen)
      rawName = rawName.replace(/[^A-Z0-9_-]/g, '');
      if (rawName.length < 2) rawName = 'PILOT';
      if (rawName.length > 10) rawName = rawName.slice(0, 10);

      // Sanity & Anti-Cheat Validation
      if (score <= 0 || score > 4000000 || time < 0 || time > 7200) {
        return res.status(400).json({ error: 'Skor atau durasi waktu tidak valid.' });
      }

      // Max score/second rate check (higher rate allowed in Hardcorez due to 2.5x multiplier)
      const maxRate = (diff === 'hardcorez' ? 550 : 280);
      if (score > 1000 && (score / Math.max(1, time)) > maxRate) {
        return res.status(400).json({ error: 'Rasio skor melebihi batas wajar.' });
      }

      const mins = Math.floor(time / 60);
      const secs = Math.floor(time % 60);
      const formattedTime = `${mins < 10 ? '0' + mins : mins}:${secs < 10 ? '0' + secs : secs}`;

      // 1. Submit to Supabase
      if (SUPABASE_URL && SUPABASE_KEY) {
        const cleanUrl = SUPABASE_URL.replace(/\/+$/, '');
        const endpoint = `${cleanUrl}/rest/v1/leaderboard`;
        const resInsert = await fetch(endpoint, {
          method: 'POST',
          headers: {
            apikey: SUPABASE_KEY,
            Authorization: `Bearer ${SUPABASE_KEY}`,
            'Content-Type': 'application/json',
            Prefer: 'return=minimal'
          },
          body: JSON.stringify([{
            name: rawName,
            score,
            time,
            formatted_time: formattedTime,
            diff
          }])
        });

        if (!resInsert.ok) {
          const errText = await resInsert.text();
          throw new Error(`Supabase insert failed (${resInsert.status}): ${errText}`);
        }

        return res.status(200).json({
          status: 'success',
          message: 'Skor berhasil dicatat di Hall of Fame (Supabase)!',
          entry: { name: rawName, score, formattedTime, diff }
        });
      }

      // 2. Submit to Redis / KV
      if (REDIS_URL && REDIS_TOKEN) {
        const entry = JSON.stringify({
          name: rawName,
          score,
          time,
          formattedTime,
          diff,
          submittedAt: Date.now()
        });

        await fetch(`${REDIS_URL}`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${REDIS_TOKEN}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(['ZADD', LEADERBOARD_KEY, score, entry])
        });

        await fetch(`${REDIS_URL}`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${REDIS_TOKEN}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(['ZREMRANGEBYRANK', LEADERBOARD_KEY, 0, -101])
        });

        return res.status(200).json({
          status: 'success',
          message: 'Skor berhasil dicatat di Hall of Fame (Redis)!',
          entry: { name: rawName, score, formattedTime, diff }
        });
      }

      // 3. Demo fallback
      return res.status(200).json({
        status: 'demo_saved',
        message: 'Mode demo: Skor diterima! Hubungkan Supabase untuk penyimpanan online permanen.',
        entry: { name: rawName, score, formattedTime, diff }
      });
    } catch (err) {
      console.error('Leaderboard submit error:', err);
      return res.status(500).json({ error: 'Gagal mencatat skor ke server.' });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
