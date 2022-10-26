Title: Fixing up URL after Auth0 login
Author: Pascal Bauermeister
Category: Programming
Tags: Auth0, Vue.js, Javascript
Date: 2022-10-26
Summary: A single page applications, after login using an IdM, may find itself left with an undesired query string. Read how to fix this.

# 1. Context

You are protecting your Single Page Application (SPA) with an
**OAuth2** identity management Service (IdM) like
[Auth0](https://auth0.com/).

After a successful login, the IdM returns the user to your web
page. Now your web page has an URL **falling back to one of a the few
allowed** callback URLs, and containing an **undesired query**.

Example:

1. User selects, say, a bookmark going to *article 42*:
   `https://mysite.com/gallery/view?article=42`

2. Because the user is logged out, the Auth0 login page is presented.

3. After successful login, the user is brought to a place which is
   obviously not displaying *article 42*:
   `https://mysite.com/?code=SOMELONGSTUFF&state=MORELONGSTUFF`,


In short, the login procedure **broke the user flow** intended by the original URL.

This article shows how:

- to eliminate the undesired query fields,
- and even better, to restore your original URL.

We are using [Auth0](https://auth0.com/) and
[Vue.js](https://vuejs.org/), but the same principle can apply
generally (I think) to OAuth2 and any web framework.

# 2. Issue details

Workflow under the hood:

1. Your page runs some code to check if the user is logged-in. If yes,
   it goes on serving the content. End of the scenario.

2. If not, your page calls the Auth0 login, passing a `redirect_uri`,
   e.g.    
   `redirect_uri=https://mysite.com/mypage?a=b`

3. then, Auth0 displays a login page to the user,

4. and once the user is validated, the Auth0 page loads the
   `redirect_uri`, returning where your page ordered.

5. As a result, the URL is now like:    
   `https://mysite.com/mypage?a=b&code=SOMESTUFF&state=MORESTUFF`    
   You can notice an addition in the query string, made by Auth0.

**Issue #1**: The `code` and `state` fields are appended by Auth0 to
the query of your `redirect_uri`.

**Issue #2**: In the case of Auth0, you cannot give an arbitrary path
in the `redirect_uri`: each possible path has to be registered in
Auth0.

- In our example, you have to register `https://mysite.com/mypage`, and if
  you have a `/mypage2` path, `https://mysite.com/mypage2` shall be
  registered too.
- This is a burden because you may want to call the login from an
  arbitrary page.

# 3. Solution concept

The idea involves two parts:

1. Given the start and end URL being `https://mysite.com/gallery/view?article=42`,
   your code in mysite.com forms a login request to Auth0, with a `redirect_uri`:

     - using no path (`https://mysite.com/`), so only one registration
       is needed in Auth0,

     - followed by a query with a dedicated field (e.g. `_return`), containing
       the real and complete desired end URL (encoded).

       E.g.    
       `redirect_uri=https://mysite.com/?_return=https%3A%2F%2Fmysite.com%2Fgallery%2Fview%3Farticle%3D42`

2. After the redirection following the login, some code in your pages
   retrieves the value of `_return`, and loads it as end URL.

A similar solution could use the browser's local storage to store the
end URL, but this is a non-reentrant solution: If you have two tabs
visiting your pages, their workflows could be garbled.


# 4. Solution details

### Part 1

```typescript
// File: main.ts
import { createApp } from 'vue'
import { createAuth0 } from '@auth0/auth0-vue';

import App from './App.vue'

import createAppRouter from "./router";  // see snippet below

const app = createApp(App)

const url =
    window.location.protocol + "//" + window.location.host +
    "?_return=" + encodeURIComponent(document.URL)

app.use(createAuth0({
    domain: auth0config.issuer,
    client_id: auth0config.client_id,
    audience: auth0config.audience,
    cacheLocation: "localstorage",
    useRefreshTokens: true,
    redirect_uri: url
}))
app.use(createAppRouter(auth0config.enabled))
app.mount('#app')
```

* **Line 11-13**: make the redirect URI from the current URL: omit the
  path and pack the current URL into the `_return` query field.

* **Line 21**: set the redirect URI into the request to Auth0.

* All other lines are non-exhaustive boilerplate to give you a bit of
  context.

### Part 2

```typescript
// File: router.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { Router } from 'vue-router'
import { authGuard } from '@auth0/auth0-vue';

export default function createAppRouter(): Router {
    const router = createRouter({
        history: createWebHistory(import.meta.env.BASE_URL),
        routes: [
            {
                path: '/whatever/path/:param',
                component: SomeView
            }
	    // etc.
        ]
    })

    router.beforeEach(authGuard)

    router.afterEach((to: any, from: any) => {
        if (to.query._return) {
            console.log("Fixing up URL using _return param:")
            console.log("-", JSON.stringify(to.query))
            console.log("- following _return :", to.query._return)
            router.replace(to.query._return)
        } else if (to.query.code && to.query.state) {
            console.log("Fixing up URL: removing code and state:")
            const query = { ...to.query }
            console.log("- removing code  :", query.code)
            console.log("- removing state :", query.state)
            delete query.code
            delete query.state
            router.replace({ path: to.path, query: query })
        }
    })

    return router
}
```

* We act in the *vue-router*, so as to be effective for all pages.

* **Line 20**: with `router.afterEach` we operate after any URL has
    been loaded or changed, so we will catch the moment that the
    `redirect_uri` is loaded.

* **Line 21**: if the query string contains `_return`, we will simply
    load it as new URL. So we will have our page positioned as before
    the login, including path and query.

* **Line 26**: this is a safeguard for other cases, when `code` and
    `state` are present: these two fields (presumably remains from
    Auth0) get removed. Note that if your page deals with two such
    fields for its own purpose, you should remove this section.