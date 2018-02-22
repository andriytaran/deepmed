import React from 'react'
import BcDiagnosis from './BcDiagnosis'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Diagnosis Summary and Treatment Recommendations'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcDiagnosis/></AppLayout>,
  }
}

export default action
