blockedFollowersScrollScript = """
    var element = document.evaluate(
        "//*[@role='dialog']/div/div/div/div/div[2] ",
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;

    if (element) {
        element.scrollTo(0, element.scrollHeight);
    }
"""

scrollScript = """
    var element = document.evaluate(
        "//*[@role='dialog']/div/div/div/div/div[3]",
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;

    if (element) {
        element.scrollTo(0, element.scrollHeight);
    }
"""

getChildElementCount = """
    var element = document.evaluate(
        "//*[@role='dialog']/div/div/div[2]/div[2]/div",
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;
    
    return element ? element.childElementCount : 50;
"""
