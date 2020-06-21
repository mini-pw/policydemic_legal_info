import React from 'react';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import SearchTableComponent from './search-table.component.js';

export default class SearchResultsListComponent extends React.Component {

    createDataForRow(source, infoDate, language, keywords, country) {
        return {
            source: source,
            infoDate: infoDate,
            language: language,
            keywords: keywords,
            country: country
        };
      }

    render() {
        return (
            <Box
                textAlign="left"
            >                
                <Typography variant="h5" style={{margin: 5}}>
                    {this.props.headerCaption}
                </Typography>

                <SearchTableComponent/>

                <Grid
                    style={{ display: 'flex', justifyContent: 'flex-start' }}
                    justify="space-around"
                >

                    <Button
                        variant="contained"
                        className="button-submit"
                        color="danger"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                        Delete
                    </Button>
                    <Button
                        variant="contained"
                        className="button-submit"
                        color="primary"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                        Download Selected
                    </Button>
                    <Button
                        variant="contained"
                        className="button-submit"
                        color="primary"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                        Add New
                    </Button>
                    <Button
                        variant="contained"
                        className="button-submit"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                        Upload JSON
                    </Button>
                </Grid>
            </Box>
        )
    }
}