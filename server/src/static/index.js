const lblUsername = document.querySelector('#lblGitHubUsername');
const authElements = document.querySelectorAll(".authorized");
const nonauthElemnents = document.querySelectorAll(".not-authorized");
const btnConnect = document.querySelector('.connect-github');
const btnSignout = document.querySelector('#btnSignout');
const hidToken = document.querySelector('#form-hidden-token');

var is_authorized = false;
const cookies = new Map()

if (btnConnect !== null) {
    btnConnect.addEventListener('click', () => {
        window.location.href = "/authorize";
    });
}

if (btnSignout !== null) {
    btnSignout.addEventListener('click', () => {
        deleteCookie('authorization');
        window.location.href = "/";
    })
}

// Create dictionary of cookies
document.cookie.split(';').forEach(cookie => {
    var pos = cookie.indexOf('=')
    var name = cookie.substr(0, pos).trim()
    var val = cookie.substr(pos + 1).trim()
    if (val !== '') {
        cookies.set(name, val)
    }
});
console.log(cookies);

//// START HELPER FUNCTIONS FOR COOKIES
function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}
function setCookie(name, value, days) {
    var d = new Date;
    d.setTime(d.getTime() + 24 * 60 * 60 * 1000 * days);
    document.cookie = name + "=" + value + ";path=/;expires=" + d.toGMTString();
}
function deleteCookie(name) { setCookie(name, '', -1); }
//// END


function setUserAuthorized(isAuthorized) {
    authElements.forEach(element => {
        element.hidden = !isAuthorized;
    })

    nonauthElemnents.forEach(element => {
        element.hidden = isAuthorized;
    })
}

async function validateAuthorizationToken() {
    const data = await getGitHubUsername()
    lblUsername.innerHTML = data['login'] !== undefined ? data['login'] : 'N/A';
    return data['status'] == 200 ? true : false;
}

async function authLogic() {
    if (cookies.has('authorization')){
        is_authorized = await validateAuthorizationToken()
        
        if (!is_authorized) {
            console.log('Invalid token');
            deleteCookie('authorization')
        } else {

            hidToken.value = cookies.get('authorization');
        }
    }
    setUserAuthorized(is_authorized);
}

/// ------------------------------
/// Start - GITHUB API FUNCTIONS
/// ------------------------------

async function getGitHubUsername() {
    const response = await fetch('https://api.github.com/user', {
        headers: {
            'Authorization': 'token ' + cookies.get('authorization'),
        },
    })

    if (response.status == 200) {
        var json = await response.json();
        json['status'] = response.status
        return json;
    } else {
        return { "status": response.status }
    }
}

async function createGitHubRepo(new_repo_name, new_repo_desc, new_repo_isprivate) {
    const response = await fetch('https://api.github.com/user/repos', {
        headers: {
            'Authorization': 'token ' + cookies.get('authorization'),
        },
        body: '{"name":"' + new_repo_name + '"}',
        method:"POST",
    })

    var json = await response.json();
    json['status'] = response.status;

    return json;
}

/// ------------------------------
/// End - GITHUB API FUNCTIONS
/// ------------------------------

authLogic();