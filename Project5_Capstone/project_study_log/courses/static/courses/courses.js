


// ===================================
// SECTION 0: Initialization code
// ===================================
document.addEventListener('DOMContentLoaded', async function() {
    
    let categories = await getObjects("Log");
    console.log(categories.results)



        
        //THIS COMMENTED CODE CREATES ONE OBJECT OF EACH MODEL
        /*
        .then(data => {categories = data})
        console.log(categories)
    let category_id = null
    let term_id = null
    let course_id = null
    let lecture_id = null
    let project_id = null

    await createCategory("======Category 1", "This is category test 1 description")
    .then(result => {console.log(result); category_id=result.id})

    await createTerm("======Term 1", "2024-02-15", "2024-07-15")
    .then(result => {console.log(result); term_id = result.id})

    await createCourse("======Course 1", "www.mit.com", 100, "N", category_id)
    .then(result => {console.log(result); course_id=result.id})

    await createLecture("======Lecture 1", "www.mit.com", "N", course_id)
    .then(result => {console.log(result); lecture_id=result.id})

    await createProject("======Project 1", "www.mit.com", "N", course_id)
    .then(result => {console.log(result); project_id=result.id})

    await createLog('ST', "======Log 1", 120, lecture_id)
    .then(result => console.log(result))
    */


})


// ===================================
// SECTION 1.0: API fetch GET
// ===================================
async function getObjects(Model){
    /** GET OBJECTS
     * Gets all the objects from given Model that belong to current user.
     * @returns {Object} An object containing all the results and a message
     * The object has the following structure:
     * {
     *    "results": "object1" // {object} An object that contains a list of all categories
     *    "message": "value2", // {string} Success or error message
     * }
     */
    
    const url_list = {
        'Category': '/get_categories',
        'Term': '/get_terms',
        'Course': '/get_courses',
        'Lecture': '/get_lectures',
        'Project': '/get_projects',
        'Log': '/get_logs',
    }

    return fetch(url_list[Model])
    .then(response => {
        if (response.status !== 200) {console.log(response.status)}
        else {console.log(response.status); return response.json()}
    })
}


// ===================================
// SECTION 1.1: API fetch CREATE
// ===================================

async function createCategory(name, description){ 
    /** CREATE CATEGORY
     * Creates a new category.
     * @param {string} name Name of category to be created
     * @param {string} description Description of category
     * @returns {Object} An object containing the success or error message. 
     * The object has the following structure:
     * {
     *    "status_code": "value1" // {string} HTTP status code. If not applicable, "NA"
     *    "message": "value2", // {string} Success message
     * }
     */

    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_category', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                name: name,
                description: description
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

async function createTerm(name, start_date, finish_date){ 
    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_term', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                name: name,
                start_date: start_date,
                finish_date: finish_date,
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

async function createCourse(name, website, hours_forecast, status, category_id){ 
    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_course', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                name: name,
                website: website,
                hours_forecast: hours_forecast,
                status: status,
                category_id: category_id,
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

async function createLecture(name, website, status, course_id){ 
    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_lecture', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                name: name,
                website: website,
                status: status,
                course_id: course_id,
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

async function createProject(name, website, status, course_id){ 
    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_project', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                name: name,
                website: website,
                status: status,
                course_id: course_id,
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

async function createLog(type, content, time_spent, course_section_id){ 
    let response = null;
    let data = null;

    try {
        // Try to get a response from server for the fetch request.
        response = await fetch('/create_log', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),  
            },
            body: JSON.stringify({
                type: type,
                content: content,
                time_spent: time_spent,
                course_section_id: course_section_id,
            }),
            credentials: 'same-origin',
        });
    } catch(error) {
        // If server did not respond.
        console.error(error);       
        return {status_code: 'NA', message:'There was no response from server.'}
    }
    
    try {
        // Try to parse the response into json
        /* If you are getting an error on this 'try', uncomment this section in order to see the error page on the console.
        console.log(error)
        error_page = await response.text();
        console.log(error_page) */
        data = await response.json();
    } catch(error) {
        // If response was not parsable
        console.log(error)
        console.log(error.message)
        return {status_code: response.status, message:'Server message was not understandable.'};
    }

    // Return depending on case
    if (!response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request failed.'};
    }
    if (response.ok && !('message' in data)){
        return {status_code: response.status, message:'Request succesful.'};
    }
    return {status_code: response.status, message: data.message, id: data.id};
}

// ===================================
// SECTION 2: Event listeners
// ===================================



// ===================================
// SECTION 3: HTML Builders
// ===================================



// ===================================
// SECTION X: Utilities
// ===================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}