

// Function to check the number of <h1> elements on the page
function checkH1Elements() {
    // Get all the <h1> elements on the page
    var h1Elements = document.getElementsByTagName('h1');

    // Check the number of <h1> elements
    if (h1Elements.length > 1) {
    console.log('Warning: There are multiple <h1> elements on the page.');
    } else if (h1Elements.length === 0) {
    console.log('Error: There are no <h1> elements on the page.');
    } else {
    console.log('The page has a single <h1> element, which is correct.');
    }
}

  // Function to check the content of the <h1> element
function checkH1Content() {
    // Get the first <h1> element on the page
    var h1Element = document.getElementsByTagName('h1')[0];

    // Check the content of the <h1> element
    if (h1Element.textContent.trim() === '') {
    console.log('Error: The <h1> element is empty.');
    } else if (h1Element.textContent.length > 100) {
    console.log('Warning: The <h1> element content is too long.');
    } else {
    console.log('The <h1> element content is valid.');
    }
}

  // Call the check functions when the page loads
window.addEventListener('load', function() {
    checkH1Elements();
    checkH1Content();
});