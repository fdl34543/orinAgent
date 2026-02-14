export default async function handler(req, res) {
  try {
    const response = await fetch(
      "https://orin-api.onrender.com/leaderboard?limit=20",
      {
        headers: {
          accept: "application/json",
        },
      }
    );

    const data = await response.json();

    res.setHeader("Cache-Control", "no-store");
    return res.status(200).json(data);
  } catch (error) {
    return res.status(500).json({
      status: "error",
      message: "Failed to fetch leaderboard",
    });
  }
}
