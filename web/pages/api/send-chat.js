export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ message: "Method not allowed" });
  }

  try {
    const { address, chat } = req.body;

    if (!address || !chat) {
      return res.status(400).json({
        status: "error",
        message: "Missing address or chat",
      });
    }

    const response = await fetch(
      "https://orin-api.onrender.com/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          address,
          chat,
        }),
      }
    );

    const data = await response.json();

    return res.status(response.status).json(data);
  } catch (error) {
    return res.status(500).json({
      status: "error",
      message: "Internal server error",
    });
  }
}
