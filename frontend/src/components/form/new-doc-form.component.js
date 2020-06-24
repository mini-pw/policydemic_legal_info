import React, { useEffect, useCallback } from 'react';
import 'date-fns';

import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';

import { KeyboardDatePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import { useForm, Controller } from "react-hook-form";
import Api from "../../common/api";

import AsyncAutocomplete from "./async-autocomplete.component";
import UploadPdfComponent from './upload-pdf.component';


export default function NewDocFormComponent({ type, onSuccessfulSend }) {
    const pdfUpload = type === "LAD";
    const [infoDate, setInfoDate] = React.useState(new Date());
    const [scrapDate, setScrapDate] = React.useState(new Date());

    const handleInfoDateChange = (date) => {
        setInfoDate(date);
        setValue("infoDate", date.toISOString());
    };
    const handleScrapDateChange = (date) => {
        setScrapDate(date);
        setValue("scrapDate", date.toISOString());
    };

    const { register, handleSubmit, setValue } = useForm();
    useEffect(() => {
        if (pdfUpload) {
            register({ name: 'pdf' });
        }
        register({ name: "keywords" });
        register({ name: "infoDate" });
        register({ name: "scrapDate" });

        register({ name: "country" });
        register({ name: "language" });
        register({ name: "translationType" });

    }, [register, pdfUpload])

    const onSubmit = useCallback(data => {
        console.log(data);

        Api.postDocument(type, data)
            .then(c => onSuccessfulSend());
    }, [type])

    return (
        <form id="new-doc-form" onSubmit={handleSubmit(onSubmit)}>
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
                <Grid container spacing={5}>
                    <Grid container item xs={12} spacing={8} justify="space-around">
                        <Grid item md={4}>
                            <TextField
                                name="webPage"
                                inputRef={register}
                                label="Web page"
                                margin="normal"
                                fullWidth
                            />
                        </Grid>
                        <Grid item md={4}>
                            <TextField
                                name="organization"
                                inputRef={register}
                                label="Organization"
                                margin="normal"
                                fullWidth
                            />
                        </Grid>
                        <Grid item md={4}>
                            <TextField
                                name="section"
                                inputRef={register}
                                label="Section"
                                margin="normal"
                                fullWidth
                            />
                        </Grid>
                    </Grid>

                    <Grid container item xs={12} spacing={8} justify="space-around">
                        <Grid item md={4}>
                            <AsyncAutocomplete
                                name="keywords"
                                collectionName="keywords"
                                style={{ width: 300 }}
                                openOnFocus
                                fullWidth
                                multiple
                                renderInput={(params) =>
                                    <TextField
                                        {...params}
                                        label="Keywords" margin="normal" />}

                                onChange={(_, opts) => setValue("keywords", opts.map(o => o.value).join(','))}
                            />
                        </Grid>
                        <Grid item md={4}>
                            <KeyboardDatePicker
                                disableToolbar
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                name="infoDate"
                                label="Info date"
                                fullWidth
                                value={infoDate}
                                onChange={handleInfoDateChange}
                                KeyboardButtonProps={{
                                    'aria-label': 'change date',
                                }}
                            />
                        </Grid>
                        <Grid item md={4}>
                            <KeyboardDatePicker
                                disableToolbar
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                name="scrapDate"
                                label="Scrap date"
                                value={scrapDate}
                                onChange={handleScrapDateChange}
                                fullWidth
                                KeyboardButtonProps={{
                                    'aria-label': 'change date',
                                }}
                            />
                        </Grid>
                    </Grid>

                    <Grid container item xs={12} spacing={8} justify="space-around">
                        <Grid item md={4}>
                            <AsyncAutocomplete
                                name="country"
                                collectionName="countries"
                                style={{ width: 300 }}
                                openOnFocus
                                onChange={(_, opt) => setValue("country", opt.value)}
                                renderInput={(params) =>
                                    <TextField
                                        {...params}
                                        inputRef={register}
                                        label="Country" margin="normal" />}
                            />
                        </Grid>
                        <Grid item md={4}>
                            <AsyncAutocomplete
                                name="language"
                                collectionName="languages"
                                inputRef={register}
                                style={{ width: 300 }}
                                openOnFocus
                                onChange={(_, opt) => setValue("language", opt.value)}
                                renderInput={(params) =>
                                    <TextField
                                        {...params}
                                        inputRef={register}
                                        label="Language" margin="normal" />}
                            />
                        </Grid>
                        <Grid item md={4}>
                            <AsyncAutocomplete
                                name="translationType"
                                collectionName="translationTypes"
                                inputRef={register}
                                style={{ width: 300 }}
                                openOnFocus
                                onChange={(_, opt) => setValue("translationType", opt.value)}
                                renderInput={(params) =>
                                    <TextField
                                        {...params}
                                        inputRef={register}
                                        label="Translation type" margin="normal" />}
                            />
                        </Grid>
                    </Grid>

                    <Grid container item xs={12}>
                        {pdfUpload ? (
                            <UploadPdfComponent setValue={setValue} name="pdf" />
                        ) : (
                                <TextField
                                    name="original-text"
                                    inputRef={register}
                                    label="Original text"
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    multiline
                                    rows={8}
                                    fullWidth
                                    placeholder=""
                                    variant="outlined"
                                />
                            )}
                    </Grid>

                    <Grid container item xs={12}>
                        <TextField
                            name="translation"
                            inputRef={register}
                            label="Translation"
                            InputLabelProps={{
                                shrink: true,
                            }}
                            multiline
                            rows={8}
                            fullWidth
                            variant="outlined"
                        />
                    </Grid>

                </Grid>
            </MuiPickersUtilsProvider>
        </form >
    );
}