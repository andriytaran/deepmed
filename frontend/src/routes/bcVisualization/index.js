import React from 'react'
import BcVisualization from './BcVisualization'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Treatment Recommendations'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcVisualization/></AppLayout>,
  }
}

export default action
