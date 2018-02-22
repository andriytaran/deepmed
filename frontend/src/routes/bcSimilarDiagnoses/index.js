import React from 'react'
import BcSimilarDiagnoses from './BcSimilarDiagnoses'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))
  const {similarDiagnoses} = store.getState().breastCancer

  let title = 'Diagnoses Similar to This Diagnosis'

  if (similarDiagnoses.similar_diagnosis && similarDiagnoses.similar_diagnosis.length) {
    title = `${similarDiagnoses.similar_diagnosis.length} ${title}`
  }

  return {
    title,
    component: <AppLayout title={title}><BcSimilarDiagnoses/></AppLayout>,
  }
}

export default action
