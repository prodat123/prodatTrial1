var clickTimes = 0;
function onSignUpButtonClick(){
    clickTimes += 1;
    document.getElementById("ProfileOptions").style.display = 'block';
    if (clickTimes > 1){
        document.getElementById("ProfileOptions").style.display = 'none';
        clickTimes = 0;
    }
}
