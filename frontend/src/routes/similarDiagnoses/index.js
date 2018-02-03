import React from 'react'
import SimilarDiagnoses from './SimilarDiagnoses'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Diagnoses Similar to This Diagnosis'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><SimilarDiagnoses/></AppLayout>,
  }
}

export default action
