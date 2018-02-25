import React from 'react'
import {getUser, logout} from '../reducers/user'
import {wsConnect} from '../reducers/breastCancer'

export const HOME_ROUTE = 'home'

export const LOGIN_ROUTE = 'login'
export const REGISTER_ROUTE = 'register'
export const LOGOUT_ROUTE = 'logout'
export const USER_ROUTE = 'user'
// Breast Cancer
export const BC_FORM_ROUTE = 'bc-form'
export const BC_DIAGNOSIS_ROUTE = 'bc-diagnosis'
export const BC_NATIONAL_STATISTICS_ROUTE = 'bc-national-statistics'
export const BC_INDIVIDUAL_STATISTICS_ROUTE = 'bc-individual-statistics'
export const BC_SIMILAR_DIAGNOSES_ROUTE = 'bc-similar-diagnoses'
export const BC_CUSTOM_ANALYTICS_ROUTE = 'bc-custom-analytics'
export const BC_RESOURCES_ROUTE = 'bc-resources'
export const BC_VISUALIZATION_ROUTE = 'bc-visualization'
export const BC_SURVIVAL_MONTHS = 'bc-survival-months'

// The top-level (parent) route
const routes = {
  path: '',
  // Keep in mind, routes are evaluated in order
  children: [
    {
      path: '/login',
      name: LOGIN_ROUTE,
      action: require('./login').default,
    },
    {
      path: '/register',
      name: REGISTER_ROUTE,
      action: require('./register').default,
    },
    // auth required routes
    {
      path: '',
      children: [
        {
          path: '/',
          name: HOME_ROUTE,
          action: require('./home').default,
        },
        {
          path: '/account',
          name: USER_ROUTE,
          action: require('./user').default,
        },
        {
          path: '/logout',
          name: LOGOUT_ROUTE,
          async action({store}) {
            await store.dispatch(logout())
            return {redirect: '/'}
          },
        },
        // Breast Cancer
        {
          path: '/breast-cancer',
          name: BC_FORM_ROUTE,
          action: require('./bcForm').default,
        },
        {
          path: '/breast-cancer/diagnosis',
          name: BC_DIAGNOSIS_ROUTE,
          action: require('./bcDiagnosis').default,
        },
        {
          path: '/breast-cancer/national-statistics',
          name: BC_NATIONAL_STATISTICS_ROUTE,
          action: require('./bcNationalStatistics').default,
        },
        {
          path: '/breast-cancer/visualization',
          name: BC_VISUALIZATION_ROUTE,
          action: require('./bcVisualization').default,
        },
        {
          path: '/breast-cancer/individual-statistics',
          name: BC_INDIVIDUAL_STATISTICS_ROUTE,
          action: require('./bcIndividualStatistics').default,
        },
        {
          path: '/breast-cancer/similar-diagnoses',
          name: BC_SIMILAR_DIAGNOSES_ROUTE,
          action: require('./bcSimilarDiagnoses').default,
        },
        {
          path: '/breast-cancer/resources',
          name: BC_RESOURCES_ROUTE,
          action: require('./bcResources').default,
        },
        {
          path: '/breast-cancer/custom-analytics',
          name: BC_CUSTOM_ANALYTICS_ROUTE,
          action: require('./bcCustomAnalytics').default,
        },
        {
          path: '/breast-cancer/survival-months',
          name: BC_SURVIVAL_MONTHS,
          action: require('./bcSurvivalMonths').default,
        },
      ],
      async action({store, next, pathname}) {
        const {loggedIn} = store.getState().user
        if (!loggedIn) {
          return {redirect: `/login?next=${pathname}`}
        }
        store.dispatch(wsConnect())
        return await next()
      },
    },
    // Wildcard routes, e.g. { path: '*', ... } (must go last)
    {
      path: '(.*)',
      action: require('./notFound').default,
    },
  ],

  async action({store, next}) {
    await store.dispatch(getUser())
    // Execute each child route until one of them return the result
    const route = await next()

    // Provide default values for title, description etc.
    route.title = `${route.title || 'DeepMed'}`
    route.description = route.description || ''

    return route
  },

}

// The error page is available by permanent url for development mode
if (__DEV__) {
  routes.children.unshift({
    path: '/error',
    action: require('./error').default,
  })
}

export default routes
