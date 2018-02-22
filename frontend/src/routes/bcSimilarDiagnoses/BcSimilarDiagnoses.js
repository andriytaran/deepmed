import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcSimilarDiagnoses.css'
import {Spin} from '../../components'
import isNil from 'lodash/isNil'

class BcSimilarDiagnoses extends React.Component {
  render() {
    const {similarDiagnoses} = this.props
    return (
      <div className={s.container}>
        <div className={s.content}>
          <div className='table-responsive'>
            <table className='table'>
              <thead>
              <tr className={s.topHeader}>
                <th colSpan={11} className={s.borderRight}>
                  <h5>Diagnosis</h5>
                </th>
                <th colSpan={3} className={s.borderRight}>
                  <h5>Treatment</h5>
                </th>
                <th colSpan={3}>
                  <h5>Outcome</h5>
                </th>
              </tr>
              <tr className={s.bottomHeader}>
                <th><h6>Age</h6></th>
                <th><h6>Ethnicity</h6></th>
                <th><h6>Size</h6></th>
                <th><h6>Grade</h6></th>
                <th><h6>ER</h6></th>
                <th><h6>PR</h6></th>
                <th><h6>HER2</h6></th>
                <th><h6>Lat</h6></th>
                <th><h6>Site</h6></th>
                <th><h6>Type</h6></th>
                <th className={s.borderRight}><h6>+Nodes</h6></th>

                <th><h6>Surgery</h6></th>
                <th><h6>Chemo</h6></th>
                <th className={s.borderRight}><h6>Radiation</h6></th>

                <th><h6>Year Dx</h6></th>
                <th><h6>Status</h6></th>
              </tr>
              </thead>
              <tbody>
              {similarDiagnoses.similar_diagnosis && similarDiagnoses.similar_diagnosis.map((item, i) =>
                <tr key={i}>
                  <td>{item['Age']}</td>
                  <td>{item['Race_group']}</td>
                  <td>{item['T_size']}</td>
                  <td>{item['Grade']}</td>
                  <td>{item['ER_status']}</td>
                  <td>{item['PR_status']}</td>
                  <td>{item['HER2_Status']}</td>
                  <td>{item['Laterality']}</td>
                  <td>{item['Primary_site']}</td>
                  <td>{item['Type']}</td>
                  <td className={s.borderRight}>{item['Nodes_Pos']}</td>

                  <td>{item['Surgery']}</td>
                  <td>{item['Chemo']}</td>
                  <td className={s.borderRight}>{item['Radiation']}</td>

                  <td>{item['Year_dx']}</td>
                  <td>{item['COD to site recode']}</td>
                </tr>
              )}
              </tbody>
            </table>
          </div>
          {isNil(similarDiagnoses.similar_diagnosis) && <Spin spinning/>}
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcSimilarDiagnoses))
