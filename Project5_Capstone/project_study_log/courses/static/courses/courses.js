


// ===================================
// SECTION 0: Initialization code
// ===================================



// ===================================
// SECTION 1: API fetch
// ===================================

/** CREATE CATEGORY
 * Creates a new category.
 * @param {string} name The first number.
 * @param {string} description The second number.
 * @returns {Object} An object containing the success or error message. 
 * The object has the following structure:
 * {
 *   "message": "value1", // {string} Success message
 *   "error": "value2", // {string} Error message'
 *   // ... more keys
 * }
 */
async function createCategory(name, description){
    const response = await fetch(/* TODO */, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            name: name,
            description: description
        }),
        credentials: 'same-origin',
    });
    return response.json();
}

// ===================================
// SECTION 2: Event listeners
// ===================================



// ===================================
// SECTION 3: HTML Builders
// ===================================