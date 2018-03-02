import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcGlobalStatistics.css'
import map_worldwide from '../../static/global_statistics/map-worldwide.jpg'
import bar_worldwide from '../../static/global_statistics/bar-worldwide.jpg'


class BcGlobalStatistics extends React.Component {
  render() {
    return (
      <div className={s.container}>
        <div className={s.imageMapWrapper}>
          <img className={s.imageMap} src={map_worldwide}/>
        </div>
        <div className={s.imageBarChartWrapper}>
          <img className={s.imageBarChart} src={bar_worldwide}/>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcGlobalStatistics))
