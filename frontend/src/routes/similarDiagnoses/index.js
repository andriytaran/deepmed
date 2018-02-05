import React from 'react'
import SimilarDiagnoses from './SimilarDiagnoses'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

let title = 'Diagnoses Similar to This Diagnosis'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))
  const {data} = store.getState().diagnosis

  if (data.similar_diagnosis && data.similar_diagnosis.length) {
    title = `${data.similar_diagnosis.length} ${title}`
  }

  return {
    title,
    component: <AppLayout title={title}><SimilarDiagnoses/></AppLayout>,
  }
}

export default action
