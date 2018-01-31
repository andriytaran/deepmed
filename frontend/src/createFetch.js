/* @flow */

type Fetch = (url: string, options: ?any) => Promise<any>;

type Options = {
  apiUrl: string,
  cookie?: string,
}

const transformFormData = (data) => {
  const str = []
  for (let p in data) {
    const key = encodeURIComponent(p)
    const value = encodeURIComponent(data[p])
    str.push(`${key}=${value}`)
  }
  return str.join('&')
}

const prepareRequestHeaders = (headers = {}, token, locale) => {
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  if (locale) {
    headers['Lang'] = locale.substring(0, 2)
  }
  return headers
}

const prepareRequestBody = (body, formData) => {
  if (formData) {
    // TODO multiform part data
    // let formDataBody = new FormData()
    // Object.keys(body).forEach((key) => {
    //   formDataBody.append(key, body[ key ])
    // })
    return transformFormData(body)
  } else {
    return JSON.stringify(body)
  }
}

/**
 * Creates a wrapper function around the HTML5 Fetch API that provides
 * default arguments to fetch(...) and is intended to reduce the amount
 * of boilerplate code in the application.
 * https://developer.mozilla.org/docs/Web/API/Fetch_API/Using_Fetch
 */
function createFetch(fetch: Fetch, {apiUrl}: Options) {
  return async (url, { token, locale, formData, ...options }) => {
    const anotherDomainRequest = url.startsWith('http')
    options.body = prepareRequestBody(options.body, formData)
    if (!anotherDomainRequest) {
      options.headers = prepareRequestHeaders({
        ...options.headers,
        Accept: 'application/json',
        'Content-Type': formData ? 'application/x-www-form-urlencoded' : 'application/json',
      }, token, locale)
    }
    try {
      const resp = await fetch(anotherDomainRequest ? url : `${apiUrl}${url}`, {
        ...options,
        headers: {
          ...options.headers,
        },
      })

      const responseText = await resp.text()
      if (responseText) {
        const responseBody = JSON.parse(responseText)
        return resp.ok ? options.success(responseBody) : options.failure(responseBody)
      } else {
        return resp.ok ? options.success({}) : options.failure({})
      }
    } catch (error) {
      return options.failure({error})
    }
  }
}

export default createFetch
