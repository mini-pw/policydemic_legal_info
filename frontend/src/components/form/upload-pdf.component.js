import React, { useCallback, useState } from 'react';
import Button from '@material-ui/core/Button';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import Pagination from '@material-ui/lab/Pagination';

import { Document, Page } from 'react-pdf';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
}));


export default function UploadPdfComponent({ name, setValue }) {
    const classes = useStyles();
    const [file, setFile] = useState();
    const [numPages, setNumPages] = useState();
    const [pageNo, setPageNo] = useState(1);

    const handleFileChange = useCallback((event) => {
        const newFile = event.target.files[0];
        setFile(newFile);
        setValue(name, newFile);
    }, [setFile, setValue]);

    const handleDocumentLoadSuccess = useCallback((obj) => {
        setNumPages(obj.numPages);
    }, [setNumPages]);

    const handlePageChange = useCallback((event, page) => {
        setPageNo(page);
    }, [setPageNo]);

    return (
        <Grid container spacing="5">
            <Grid item xs={12}>
                <div className={classes.root}>
                    <input
                        accept=".pdf"
                        className={classes.input}
                        name={name}
                        id="contained-button-file"
                        type="file"
                        onChange={handleFileChange}
                    />
                    <label htmlFor="contained-button-file">
                        <Button
                            variant="contained"
                            color="default"
                            endIcon={<CloudUploadIcon />}
                            component="span"
                        >
                            Upload document
                </Button>
                    </label>
                </div>
            </Grid>
            {file && (
                <Grid item xs={12}>
                    <Card> 
                        <CardHeader title="PDF Preview" />
                        <CardContent style={{ display: "flex", alignItems: "center", justifyContent: "center"}}>
                            <Document file={file} onLoadSuccess={handleDocumentLoadSuccess}>
                                <Page pageNumber={pageNo} />
                            </Document>
                        </CardContent>
                        <CardActions style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                            {numPages && (
                                <Pagination 
                                    page={pageNo}
                                    count={numPages}
                                    onChange={handlePageChange}
                                    color="primary"
                                 />
                            )}
                        </CardActions>
                    </Card>
                </Grid>
            )}
        </Grid>

    )
}