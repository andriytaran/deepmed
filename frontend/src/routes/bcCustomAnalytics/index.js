import React from 'react'
import BcCustomAnalytics from './BcCustomAnalytics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  const title = 'Custom Analytics'

  return {
    title,
    component: <AppLayout title={title}><BcCustomAnalytics/></AppLayout>,
  }
}

export default action
