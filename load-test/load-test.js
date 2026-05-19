import http from "k6/http";
import { sleep, check } from "k6";

export const options = {
  iterations: 20,
  vus: 5,
  duration: "30s",

  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<15000"],
  },
};

const prompts = [
  "Explain artificial intelligence",
  "Write 10 lines about cows",
  "What is Kubernetes?",
  "Explain Docker networking",
  "Write a short essay on cloud computing",
  "What is observability?",
  "Explain machine learning",
  "What is Grafana used for?"
];

export default function () {

  const prompt =
    prompts[Math.floor(Math.random() * prompts.length)];

    const payload = JSON.stringify({
      messages: [
        {
          role: "user",
          content: prompt
        }
      ],
      model: "qwen2.5-coder:7b"
    });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = http.post(
    "http://backend:8000/chat",
    payload,
    params
  );

  check(response, {
    "status is 200": (r) => r.status === 200,
  });

  console.log(
    `Prompt: ${prompt} | Status: ${response.status}`
  );

  sleep(2);
}