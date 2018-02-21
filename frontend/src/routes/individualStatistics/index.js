import React from 'react'
import IndividualStatistics from './IndividualStatistics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Personalized Diagnosis and Treatment Statistics'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><IndividualStatistics/></AppLayout>,
  }
}

export default action
