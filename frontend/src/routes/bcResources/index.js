import React from 'react'
import BcResources from './BcResources'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

const title = 'Most Relevant Resources DeepMed has Reviewed that May Interest You'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title,
    component: <AppLayout title={title}><BcResources/></AppLayout>,
  }
}

export default action
