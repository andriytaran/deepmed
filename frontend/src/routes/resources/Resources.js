import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Resources.scss'
import { Line, Bar, Pie, HorizontalBar } from 'react-chartjs-2';

class Resources extends React.Component {
  render() {
    return (
      <div className="container container-full" data-children="same-height">

        <div className="row">
          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">
              <h2 className="push-top-2 push-bot-2">Google Links <span className="text-light">(17)</span></h2>
              <div className="custom-scroll-bar-wrapper max-height-300">
                <div className="scrollbar-inner">
                  <div className="push-top-3">
                    <a href="#">Triple-Negative Breast Cancer | Breastcancer.org</a>
                    <p>Your pathology report may say that the breast cancer cells tested negative
                      for estrogen receptors (ER-), progesterone receptors (PR-), and HER2
                      (HER2-)...</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">
              <h2 className="push-top-2 push-bot-2">Links to Pubmed Studies Studies <span className="text-light">(12)</span>
              </h2>
              <div className="custom-scroll-bar-wrapper max-height-300">
                <div className="scrollbar-inner">
                  <div className="push-top-3">
                    <a href="#">Breast cancer survival in Soweto, Johannesburg, South Africa: A
                      receptor-defined cohort of women diagnosed from 2009 to 11.</a>
                    <p>Cubasch H, Dickens C, Joffe M, Duarte R, Murugan N, Tsai Chih M, Moodley K,
                      Sharma V, Ayeni O, Jocobson JS, Neugut AI, McCormack V, Ruff P.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">
              <h2 className="push-top-2 push-bot-2">Blogs and Posts RegardingSimilar Cancer Diagnosis <span
                className="text-light">(11)</span></h2>
              <div className="custom-scroll-bar-wrapper max-height-300">
                <div className="scrollbar-inner">
                  <div className="push-top-3">
                    <a href="#">Starting Chemo in September 2017</a>
                    <p>MKN, I am not triple negative but I did have a BMX back in July with tissue
                      expanders. It was not... (In the 'Chemotherapy - Before, During, and After'
                      Forum)</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">
              <h2 className="push-top-2 push-bot-2">Most Recent News Articles <span
                className="text-light">(12)</span></h2>
              <div className="custom-scroll-bar-wrapper max-height-300">
                <div className="scrollbar-inner">
                  <div className="push-top-3">
                    <div className="display-table">
                      <div className="display-table-cell">
                        <div className="post-thumb"
                             style={{backgroundImage: `url('${require('../../static/news-placeholder.png')}')`}}>
                        </div>
                      </div>
                      <div className="display-table-cell pad-left-1">
                        <a href="#">Tumor Fraction in cfDNA Sample Predicts Survival in...</a>
                        <p>The tumor fraction of a cell-free DNA (cfDNA) sample may predict
                          survival among patients with metastatic triple-negative breast
                          cancer (TNBC)...</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(Resources))
