function setCookie(nameContainerID, valueContainerID) {
    const nameInput = document.getElementById(nameContainerID);
    const valueInput = document.getElementById(valueContainerID);

    if (nameInput && valueInput) {
        const name = nameInput.value;
        const value = valueInput.value;

        if (name && value) {
            document.cookie = `${name}=${value}`;
            alert("Cookie set");
        }
    }
};


function showCookies() {
    alert(document.cookie);
}
