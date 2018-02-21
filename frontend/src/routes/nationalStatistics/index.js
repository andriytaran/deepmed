import React from 'react'
import NationalStatistics from './NationalStatistics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'National Breast Cancer Statistics'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><NationalStatistics/></AppLayout>,
  }
}

export default action
