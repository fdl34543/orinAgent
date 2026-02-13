export default async function handler(req, res) {
  try {
    const { limit = "50" } = req.query;

    const response = await fetch(
      `https://orin-api.onrender.com/chat/all?limit=${limit}`,
      {
        headers: {
          accept: "application/json",
        },
      }
    );

    const data = await response.json();

    res.setHeader("Cache-Control", "no-store");

    return res.status(response.status).json(data);
  } catch (error) {
    return res.status(500).json({
      status: "error",
      message: "Internal server error",
    });
  }
}
