const form = document.querySelector("#paper-form");
const result = document.querySelector("#result");
const serviceStatus = document.querySelector("#service-status");

async function checkServiceHealth() {
  try {
    const response = await fetch("http://localhost:8000/health");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const serviceName = data.service ?? "Paper-Reading-Agent";
    serviceStatus.textContent = `后端状态：可用 (${serviceName})`;
    serviceStatus.classList.remove("status-waiting", "status-error");
    serviceStatus.classList.add("status-ok");
  } catch (error) {
    serviceStatus.textContent = `后端状态：不可用 (${error.message})`;
    serviceStatus.classList.remove("status-waiting", "status-ok");
    serviceStatus.classList.add("status-error");
  }
}

function renderResult(data) {
  const summary = data.summary ?? {};
  const glossary = Array.isArray(data.glossary) ? data.glossary : [];
  const learningPlan = Array.isArray(data.learning_plan) ? data.learning_plan : [];
  const artifacts = data.artifacts ?? {};
  const source = data.source ?? {};

  const glossaryText = glossary.length
    ? glossary
        .map((item, index) => `${index + 1}. ${item.term}：${item.explanation}`)
        .join("\n")
    : "无";

  const planText = learningPlan.length
    ? learningPlan
        .map((item, index) => `${index + 1}. [${item.stage}] ${item.task}`)
        .join("\n")
    : "无";

  return [
    `论文ID：${data.paper_id ?? "-"}`,
    `标题：${data.title ?? "-"}`,
    `来源：${source.type ?? "-"}（正文字符数 ${source.markdown_body_chars ?? 0}）`,
    "",
    "一、论文总结",
    `- 研究问题：${summary.research_problem ?? "-"}`,
    `- 方法：${summary.method ?? "-"}`,
    `- 贡献：${summary.contribution ?? "-"}`,
    `- 局限：${summary.limitation ?? "-"}`,
    "",
    "二、术语表",
    glossaryText,
    "",
    "三、学习计划",
    planText,
    "",
    "四、文件位置",
    `- paper_dir：${artifacts.paper_dir ?? "-"}`,
    `- output_dir：${artifacts.output_dir ?? "-"}`,
    `- analysis_json：${artifacts.analysis_json ?? "-"}`,
    `- reading_note：${artifacts.reading_note ?? "-"}`,
  ].join("\n");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    title: document.querySelector("#paper-title").value.trim(),
    abstract: document.querySelector("#paper-abstract").value.trim(),
    markdown_body: document.querySelector("#paper-markdown-body").value.trim(),
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
    result.textContent = renderResult(data);
  } catch (error) {
    result.textContent = `请求失败：${error.message}`;
  }
});

checkServiceHealth();
