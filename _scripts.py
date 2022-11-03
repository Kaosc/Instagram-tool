scrollScript = """ document.evaluate("//*[@role='dialog']/div/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.lastElementChild.scrollTo(0, document.evaluate("//*[@role='dialog']//ul", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.lastElementChild.scrollHeight) """
scrollPage = """window.scrollTo(0, document.body.scrollHeight);"""
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
if(!skip) {
  list[0].click();
} else if (skip && list.length === 1 && list[0].innerText === "Follow") {
  list[0].click();
}
"""
unFollowUser = """
const buttons = await document.querySelectorAll('button');
buttons[1].click();
"""