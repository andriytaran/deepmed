import React from 'react'
import {connect} from 'react-redux'
import s from './BcVisualization.css'
import {Col, Row, Spin} from '../../components'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import cn from 'classnames'
import isNil from 'lodash/isNil'
import Tab from 'react-bootstrap/lib/Tab'
import Tabs from 'react-bootstrap/lib/Tabs'
import isEmpty from 'lodash/isEmpty'
import {TUMOR_GRADES} from '../../constants'
import overview from '../../static/visualization/overview.png'
import mastectomy1 from '../../static/visualization/mastectomy_1.png'
import mastectomy2 from '../../static/visualization/mastectomy_2.png'
import mastectomy3 from '../../static/visualization/mastectomy_3.png'
import lumpectomy1 from '../../static/visualization/lumpectomy_1.png'
import lumpectomy2 from '../../static/visualization/lumpectomy_2.png'
import lumpectomy3 from '../../static/visualization/lumpectomy_3.png'


const SurgeryTypesTable = ({items = [], visibleRowIndex}) =>
  <div className='table-responsive'>
    <table className={cn('table', s.SurgeryTypesTable)}>
      <thead>
      <tr className={s.SurgeryTypesTopHeader}>
        <th colSpan={3}><h6>SURGERY</h6></th>
      </tr>
      <tr className={s.SurgeryTypesBottomHeader}>
        <th><h6>RECOMMENDATION</h6></th>
        <th><h6>TYPE</h6></th>
        <th className={s.borderRight}><h6>CONFIDENCE</h6></th>
      </tr>
      </thead>
      <tbody>
      {items[visibleRowIndex] ? (
        <tr>
          <td>{items[visibleRowIndex].surgery}</td>
          <td>{items[visibleRowIndex].type}</td>
          <td
            className={s.borderRight}>{items[visibleRowIndex].surgery_confidence_level}{items[visibleRowIndex].type === 'N/A' ? '' : '%'} </td>
        </tr>
      ) : (
        <tr>
          <td colSpan={7} style={{textAlign: 'center'}}>N/A</td>
        </tr>
      )}
      </tbody>
    </table>
  </div>

const surgery_images = {
  'mastectomy': [
    overview,
    mastectomy1,
    mastectomy2,
    mastectomy3,
  ],
  'lumpectomy': [
    overview,
    lumpectomy1,
    lumpectomy2,
    lumpectomy3,
  ]
}

class BcVisualization extends React.Component {
  state = {
    tab: 0,
    surgery_images: null,
  }

  componentDidMount() {
    let s_type = null
    let s_images = null
    if (this.props.diagnosis.overall_plans !== undefined) {
      if (this.props.diagnosis.overall_plans[0] !== undefined) {
        s_type = this.props.diagnosis.overall_plans[0].type
      }
    }
    if (s_type === 'Lumpectomy') {
      s_images = surgery_images.lumpectomy
    } else if (s_type === 'Mastectomy') {
      s_images = surgery_images.mastectomy
    }
    this.setState({
      surgery_images: s_images
    })
  }

  changeTab = (tab) => {
    let s_type = null
    let s_images = null
    if (this.props.diagnosis.overall_plans !== undefined) {
      if (this.props.diagnosis.overall_plans[tab] !== undefined) {
        s_type = this.props.diagnosis.overall_plans[tab].type
      }
    }
    if (s_type === 'Lumpectomy') {
      s_images = surgery_images.lumpectomy
    } else if (s_type === 'Mastectomy') {
      s_images = surgery_images.mastectomy
    }
    this.setState({
      tab: tab,
      surgery_images: s_images
    })
  }

  render() {
    const {tab, surgery_images} = this.state
    const {diagnosis} = this.props

    return (
      <div className='container container-full'>
        <div className='row'>
          <div className='col-md-12'>

            <div className={s.card}>
              <h2 className={s.cardHeader}>Recommended Treatment Plans</h2>
              <section className={s.section}>
                <div className={s.sectionContent}>
                  <Tabs
                    activeKey={tab}
                    onSelect={this.changeTab}
                    id='SurgeryTypesTabs'
                    justified
                    animation={false}
                    className={s.SurgeryTypesTabs}
                  >
                    <Tab eventKey={0} title='PREFERRED RECOMMENDATION'>
                      <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={0}/>
                    </Tab>
                    <Tab eventKey={1} title='ALTERNATIVE RECOMMENDATION'>
                      <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={1}/>
                    </Tab>
                  </Tabs>
                </div>
              </section>
              {(!isEmpty(diagnosis.overall_plans) && !isEmpty(surgery_images)) && (
                <div>
                  {surgery_images.map((item, i) =>
                    <img key={i} className={s.surgeryImage} src={item}/>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcVisualization))
