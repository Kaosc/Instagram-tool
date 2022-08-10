scrollScript = """ document.evaluate("//*[@role='dialog']/div/div/div/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.lastElementChild.scrollTo(0, document.evaluate("//*[@role='dialog']/div/div/div/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.lastElementChild.scrollHeight) """
followUser = """ 
let list = [];
let skip = false;
await document.querySelectorAll('button').forEach((item) => {
  if (item.innerText === "Message" || item.innerText === "Requested") {
    skip = true
  } else if (item.innerText !== "") {
    list.push(item)
  }
});
console.log(list)
if(!skip) {
  list[0].click();
} else if (!skip && list.length === 1 && list[0].innerText === "Follow") {
  list[0].click();
}
"""