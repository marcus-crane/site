// Some small helper scripts for the site

(function() {
    if (location.pathname !== '/') {
        category = location.pathname.split('/').filter(e => e !== '')[0];
        navItem = document.querySelector('#' + category)
        navItem.innerHTML = '[ ' + category + ' ]'
    }
})()