export default async function handler(req, res) {
  const { name } = req.query;

  if (!name) {
    return res.status(400).json({
      status: "error",
      message: "Agent name required",
    });
  }

  try {
    const response = await fetch(
      `https://orin-api.onrender.com/agent/name/${name}`,
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
      message: "Failed to fetch agent",
    });
  }
}
