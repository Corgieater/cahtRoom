const sub = document.querySelector("#sub");
sub.addEventListener("click", async (e) => {
  e.preventDefault();
  // 拿表單資訊
  const formData = new FormData(document.querySelector("#form"));
  // 上傳資料
  let req = await fetch("/upload", {
    method: "POST",
    body: formData,
  });
  location.reload();
});

// make messages apear
async function makeMessages(fileName, text, sequence = "normal") {
  let outputArea = document.querySelector(".outputArea");
  let div = document.createElement("div");
  if (fileName !== null) {
    let img = document.createElement("img");
    img.src = `http://d4u16azcwb6ha.cloudfront.net/${fileName}`;
    div.append(img);
  }
  let p = document.createElement("p");
  p.textContent = text;
  div.append(p);
  div.classList.add("messageFrame");
  if (sequence === "normal") {
    outputArea.append(div);
  } else {
    outputArea.insertBefore(div, outputArea.firstChild);
  }
}

async function getOldData() {
  let req = await fetch("/getolddata");
  let res = await req.json();
  return res;
}

async function showOldMessages() {
  let info = await getOldData();
  for (let i = 0; i < info["data"]["text"].length; i++) {
    makeMessages(info["data"]["img"][i], info["data"]["text"][i]);
  }
}

showOldMessages();
