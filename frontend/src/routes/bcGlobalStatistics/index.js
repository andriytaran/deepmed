import React from 'react'
import BcGlobalStatistics from './BcGlobalStatistics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Global Breast Cancer Statistics'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcGlobalStatistics/></AppLayout>,
  }
}

export default action
