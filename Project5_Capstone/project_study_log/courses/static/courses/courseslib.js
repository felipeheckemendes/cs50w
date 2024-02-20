



// ===================================
// SECTION 1.0: API fetch GET
// ===================================
async function getObjects(Model){
    /** GET OBJECTS
     * Gets all the objects from given Model that belong to current user.
     * @returns {Object} An object containing all the results and a message
     * The object has the following structure:
     * {
     *    "results": "object1" // {object} A JSON object with all the objects from chosen Model
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
function buildCategoryHTML(category) {
    /**Create an HTML object with the category
     * Parameters:
     * @argument {category} is a JSON object that representes the category. 
     * Should contain the following fields:
     * id, category, name, description, user, total_courses, finished_courses,
     * hours_forecast, total_time_spent.
     * 
     * @returns {HTML object} An HTML object that can be appended to document
     */
       
        CHECK_ICON_SRC = document.body.dataset.iconUrl

        // Create check icon element
        let check_icon = document.createElement('img');
        check_icon.className = "pe-2"
        check_icon.setAttribute('alt', ".")
        check_icon.setAttribute('src', CHECK_ICON_SRC)

        // Create category_description
        category_description = document.createElement('span')
        category_description.className = "card-subtitle small text-muted"
        category_description.innerHTML = category.description

        // Create category description div
        category_description_div = document.createElement('div')
        category_description_div.className = "d-none d-md-block col-sm-12 pt-0 pb-1 px-3"
        category_description_div.append(category_description)

        // Create category description div parent
        category_description_div_parent = document.createElement('div')
        category_description_div_parent.className = "row g-0 d-flex"
        category_description_div_parent.append(category_description_div)

        // Create courses status div        
        let course_status = document.createElement('span')
        course_status.className = "text-muted small"
        course_status.append(check_icon)
        course_status.innerHTML += category.finished_courses + '/' + category.total_courses + ' Courses'

        let course_status_div = document.createElement('div')
        course_status_div.className = "col col-12 col-md-4 col-lg py-1 px-3 d-flex align-items-center border-bottom"
        course_status_div.append(course_status)

        // Create Hours spent so far div
        let hours_spent = document.createElement('span')
        hours_spent.className = "text-muted small"
        hours_spent.innerHTML += "Hours spent so far: " + category.total_time_spent + "h"

        let hours_spent_div = document.createElement('div')
        hours_spent_div.className = "col-auto col-6 col-md-4 col-lg-auto border-end d-flex py-1 px-3 m-0 border-bottom align-items-center"
        hours_spent_div.append(hours_spent)

        // Create Expected study time div
        let expected_study_time = document.createElement('span')
        expected_study_time.className = "text-muted small"
        expected_study_time.innerHTML += "Expected study time: " + category.hours_forecast + "h"

        let expected_study_time_div = document.createElement('div')
        expected_study_time_div.className = "col-auto col-6 col-md-4 col-lg-auto border-end d-flex py-1 px-3 m-0 border-bottom align-items-center"
        expected_study_time_div.append(expected_study_time)

        // Create Category Title div
        let category_title = document.createElement('h5')
        category_title.className = "card-title p-0 pb-1 m-0 pe-2"
        category_title.innerHTML = category.name
        
        let category_title_div = document.createElement('div')
        category_title_div.className = "col-12 col-lg-auto pt-2 pb-0 px-3 align-items-center border-bottom"
        category_title_div.append(category_title)

        // Create category header Div
        let category_header_div = document.createElement('div')
        category_header_div.className = "row d-flex g-0 p-0 align-items-stretch"
        category_header_div.append(category_title_div, expected_study_time_div, hours_spent_div, course_status_div)

        // Create card header div
        let card_header_div = document.createElement('div')
        card_header_div.className = "card-header p-0"
        card_header_div.append(category_header_div, category_description_div_parent)

        // Create card div
        let card_div = document.createElement('div')
        card_div.className = "card mb-1"
        card_div.append(card_header_div)
        card_div.id = "category-" + category.id
        return card_div

}


function buildCourseHTML(course) {
    /**Create an HTML object with the course
     * Parameters:
     * @argument {course} is a JSON object that representes the course. 
     * Should contain the following fields:
     * id, category, name, status, user, website, total_lectures, finished_lectures,
     * total_projects, finished_projects, hours_forecast, total_time_spent
     * 
     * @returns {HTML object} An HTML object that can be appended to document
     */
       
        CHECK_ICON_SRC = document.body.dataset.iconUrl

        // Create check icon element
        let check_icon = document.createElement('img');
        check_icon.className = "pe-2"
        check_icon.setAttribute('alt', ".")
        check_icon.setAttribute('src', CHECK_ICON_SRC)
        
        // Create project status div
        let project_status = document.createElement('span')
        project_status.className = "text-muted small pe-3 mx-auto"
        project_status.append(check_icon)
        project_status.innerHTML += course.finished_projects + '/' + course.total_projects + ' Projects'

        let project_status_div = document.createElement('div')
        project_status_div.className = "col-6 col-lg py-1 px-3 border-top d-flex"
        project_status_div.append(project_status)

        // Create lecture status div        
        let lecture_status = document.createElement('span')
        lecture_status.className = "text-muted small pe-3 mx-auto"
        lecture_status.append(check_icon)
        lecture_status.innerHTML += course.finished_lectures + '/' + course.total_lectures + ' Lectures'

        let lecture_status_div = document.createElement('div')
        lecture_status_div.className = "col-6 col-lg border-end py-1 px-3 border-top d-flex"
        lecture_status_div.append(lecture_status)

        // Create hours spent so far div
        let hours_spent = document.createElement('span')
        hours_spent.className = "text-muted small mx-auto"
        hours_spent.innerHTML += "Hours spent so far: " + course.total_time_spent + "h"
        
        let hours_spent_div = document.createElement('div')
        hours_spent_div.className = "col-6 col-lg border-end d-flex py-1 px-3 border-top"
        hours_spent_div.append(hours_spent)


        // Create expected study time div
        let expected_study_time = document.createElement('span')
        expected_study_time.className = "text-muted small mx-auto"
        expected_study_time.innerHTML += "Expected study time: " + course.hours_forecast + "h"
        
        let expected_study_time_div = document.createElement('div')
        expected_study_time_div.className = "col-6 col-lg border-end d-flex py-1 px-3 border-top"
        expected_study_time_div.append(expected_study_time)

        // Create status div
        let status_div = document.createElement('div')
        status_div.className = "row g-0 d-flex align-items-center"
        status_div.append(expected_study_time_div, hours_spent_div, lecture_status_div, project_status_div)

        // Create website link anchor
        let website_link = document.createElement('a')
        website_link.href = course.website
        website_link.innerHTML = "Website"

        // Create Course Title
        let course_title = document.createElement('h6')
        course_title.className = "card-title p-0 pb-1 m-0"
        course_title.innerHTML = course.name + " ("
        course_title.append(website_link)
        course_title.innerHTML += ")"

        
        // Create Course title div
        course_title_div = document.createElement('div')
        course_title_div.className = "col-12 pt-2 pb-0 px-3 card-header"
        course_title_div.append(course_title)

        // Create course card div
        course_card_div = document.createElement('div')
        course_card_div.className = "card mb-1"
        course_card_div.setAttribute('data-course-id', course.id)
        course_card_div.append(course_title_div, status_div)
        
        return course_card_div

    }
    
  
function buildCourseSectionHTML(course_section) {
    /**Create an HTML object with the course_section
     * Parameters:
     * @argument {course} is a JSON object that representes the course_section. 
     * Should contain the following fields:
     * id, category, name, status, user, website, total_time_spent
     * @returns {HTML object} An HTML object that can be appended to document
     */
       
        CHECK_ICON_SRC = document.body.dataset.iconUrl

        // Create check icon element
        let check_icon = document.createElement('img');
        check_icon.className = "pe-2"
        check_icon.setAttribute('alt', ".")
        check_icon.setAttribute('src', CHECK_ICON_SRC)
        
        // Create status  div
        let status = document.createElement('span')
        if (course_section.status = "Not started"){
            status.className = "badge text-bg-secondary mx-auto"    
        } else if (course_section.status = "Started") {
            status.className = "badge text-bg-primary mx-auto"
        } else if (course_section.status = "Finished") {
            status.className = "badge text-bg-dark mx-auto"
        }
        status.innerHTML += course_section.status
        
        let status_div = document.createElement('div')
        status_div.className = "col-auto py-2 px-3"
        status_div.append(status)

        console.log(status_div)

        // Create website link anchor
        let website_link = document.createElement('a')
        website_link.href = course_section.website
        website_link.innerHTML = "Website"

        // Create Course section Title
        let course_section_title = document.createElement('h6')
        course_section_title.className = "card-title pb-2 m-0"
        course_section_title.innerHTML = course_section.name + " ("
        course_section_title.append(website_link)
        course_section_title.innerHTML += ")"

        
        // Create Course section title div
        course_section_title_div = document.createElement('div')
        course_section_title_div.className = "col-auto pt-2 pb-0 px-3"
        course_section_title_div.append(course_section_title)
        
        console.log(course_section_title_div)

        // Create course section row
        course_section_row = document.createElement('div')
        course_section_row.className = "row d-flex p-0 g-0"
        course_section_row.append(course_section_title_div, status_div)

        // Create course section card div
        course_section_card_div = document.createElement('div')
        course_section_card_div.className = "card mb-1"
        course_section_card_div.setAttribute('data-course-id', course_section.id)
        course_section_card_div.append(course_section_row)

        console.log(course_section_card_div)
        return course_section_card_div

    }
    



function addCollapse(parent_card, child_element){
    COLLAPSE_ICON_SRC = document.body.dataset.collapseUrl
    parent_id = parent_card.id
    // Create button_img
    let button_img = document.createElement('img')
    button_img.setAttribute('alt', ".")
    button_img.setAttribute('src', COLLAPSE_ICON_SRC)

    // Create collapse button
    let collapse_button = document.createElement('button')
    collapse_button.className = "btn btn-light py-0 px-1"
    collapse_button.setAttribute("data-bs-toggle", "collapse")
    collapse_button.setAttribute("data-bs-target", "#" + parent_id+"-collapse")
    collapse_button.append(button_img)

    // Create collapse button div
    let collapse_button_div = document.createElement('div')
    collapse_button_div.className = "d-grid gap-2"
    collapse_button_div.append(collapse_button)

    parent_card.append(collapse_button_div)

    // Create collapse div
    let collapse_div = document.createElement('div')
    collapse_div.className="collapse"
    collapse_div.id = parent_id+"-collapse"

    // Create row and column div
    let row_div = document.createElement('div')
    row_div.className = "row"
    let col_div_blank = document.createElement('div')
    col_div_blank.className = "col-1"
    let col_div_content = document.createElement('div')
    col_div_content.className = "col col-11"
    col_div_content.append(child_element)
    row_div.append(col_div_blank, col_div_content)
    collapse_div.append(row_div)

    tree = document.createDocumentFragment();

    tree.append(parent_card, collapse_div)

    return tree

}

    

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