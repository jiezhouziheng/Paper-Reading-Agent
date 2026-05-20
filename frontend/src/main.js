const form = document.querySelector("#paper-form");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    title: document.querySelector("#paper-title").value.trim(),
    abstract: document.querySelector("#paper-abstract").value.trim(),
  };

  result.textContent = "分析中...";

  try {
    const response = await fetch("http://localhost:8000/api/papers/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    result.textContent = `请求失败：${error.message}`;
  }
});
