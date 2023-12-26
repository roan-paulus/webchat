"use strict"


const destroyFlashBtn = document.querySelector("#destroy-flash-button");
if (destroyFlashBtn !== null) {
    destroyFlashBtn.addEventListener("click", (e) => {
        document.querySelector("#header-flash-message").remove();
    });
}

