import React from 'react'
import BcUSStatistics from './BcUSStatistics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'U.S. Breast Cancer Statistics'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcUSStatistics/></AppLayout>,
  }
}

export default action
