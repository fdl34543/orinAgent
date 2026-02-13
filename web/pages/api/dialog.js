export default async function handler(req, res) {
  try {
    const { newest = "true", limit = "50" } = req.query;

    const response = await fetch(
      `https://orin-api.onrender.com/dialog/all?newest=${newest}&limit=${limit}`,
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
        message: "Failed to fetch dialog",
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
