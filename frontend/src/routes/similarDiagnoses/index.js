import React from 'react'
import SimilarDiagnoses from './SimilarDiagnoses'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'Similar Diagnoses',
    component: <AppLayout><SimilarDiagnoses/></AppLayout>,
  }
}

export default action
