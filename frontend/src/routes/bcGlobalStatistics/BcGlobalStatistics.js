import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcGlobalStatistics.css'
import {Col} from '../../components'
import map_worldwide from '../../static/global_statistics/map-worldwide.jpg'
import bar_worldwide from '../../static/global_statistics/bar-worldwide.jpg'
const chart_images = [
  map_worldwide,
  bar_worldwide
]

class BcGlobalStatistics extends React.Component {
  render() {
    return (
      <div className={s.container}>
          <Col>
            <div className={s.card}>
              {chart_images.map((item, i) =>
                <img className={s.image} src={item}/>
              )}
            </div>
          </Col>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcGlobalStatistics))
