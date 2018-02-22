import React from 'react'
import BcIndividualStatistics from './BcIndividualStatistics'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Personalized Diagnosis and Treatment Statistics'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcIndividualStatistics/></AppLayout>,
  }
}

export default action
