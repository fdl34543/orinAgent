export default async function handler(req, res) {
  try {
    const { limit = "50", newest = "true" } = req.query;

    const response = await fetch(
      `https://orin-api.onrender.com/action/history/all?limit=${limit}&newest=${newest}`,
      {
        headers: {
          accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        status: "error",
        message: "Failed to fetch activity",
      });
    }

    return res.status(200).json(data);
  } catch (error) {
    return res.status(500).json({
      status: "error",
      message: "Internal server error",
    });
  }
}
