import React from 'react'
import BcEstimatedSurvival from './BcEstimatedSurvival'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  const title = 'Estimated Survival'

  return {
    title,
    component: <AppLayout title={title}><BcEstimatedSurvival/></AppLayout>,
  }
}

export default action
