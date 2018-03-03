import React from 'react'
import BcSurvivalMonths from './BcSurvivalMonths'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  const title = 'Survival Months'

  return {
    title,
    component: <AppLayout title={title}><BcSurvivalMonths/></AppLayout>,
  }
}

export default action
