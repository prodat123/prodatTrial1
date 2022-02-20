var clickCounter = 0

function clickOnComment(count){
    clickCounter += 1;
    commentButtonClick = document.getElementById(count);
    commentButtonClick.style.display = 'block'
    if (clickCounter > 1){
        commentButtonClick.style.display = 'none';
        clickCounter = 0;
    }

}

