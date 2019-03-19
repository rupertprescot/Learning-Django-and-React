import React, {Component} from 'react';
import Container from "react-bootstrap/es/Container";
import Button from "react-bootstrap/es/Button";
import axios from "axios";
import Col from "react-bootstrap/Col";
import ProgressBar from "react-bootstrap/ProgressBar";
import Image from "react-bootstrap/es/Image";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            apiResponse: [],
            selectedFile: undefined,
            loaded: 0,
            images: []
        }
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:5000/collection_images')
        .then((res) => {
            console.log(res.data);
            this.setState({ images: res.data })
        })
    }


    handleUpload = () => {
        var formData = new FormData();
        formData.append('image', this.state.selectedFile, this.state.selectedFile.name);
        axios.post('http://127.0.0.1:5000/find_image',
            formData, {
                onUploadProgress: progressEvent => {
                    this.setState({
                        apiResponse: [],
                        loaded: (progressEvent.loaded / progressEvent.total * 100)
                    })
                }
            }
        )
            .then((res) => {
                this.setState({
                    apiResponse: res.data,
                    loaded: 0
                })
            })
            .catch((reason => {
                this.setState({
                    apiResponse: [{ message: reason.toString() } ],
                    loaded: 0
                })
            }))
    };

    handleSelectFile = (e) => {
        this.setState({selectedFile: e.target.files[0]})
    };

    render() {
        return (
            <Container>
                <h1>Hackday Face Finder</h1>
                <Col>
                    {
                        Object.keys(this.state.images).length > 0 ?
                            Object.entries(this.state.images).map((pair) => {
                                const apiResponse = this.state.apiResponse;
                                const highlighted = apiResponse && apiResponse.map(r => r.name)[0] === pair[0];
                                const style = highlighted ? { height: 200, backgroundColor: 'red' } : {height: 200};
                                return <Image src={pair[1]} id={pair[0]} key={pair[0]} thumbnail style={style} />
                            })
                            : ''
                    }<p/>
                    <input type="file" id="image" name="image" className="btn btn-outline-warning" onChange={this.handleSelectFile}/>&nbsp;
                    <Button onClick={this.handleUpload} variant="warning">Upload and Compare</Button><br/>
                    <br/>
                    {this.state.selectedFile && this.state.loaded > 0 ?
                        <ProgressBar striped variant="success" now={this.state.loaded}/> : ''
                    }
                    <p>{this.state.apiResponse.map(r => r.message)}</p>
                    {this.state.selectedFile ?
                        <img src={URL.createObjectURL(this.state.selectedFile)} alt="original image" style={{ width: 500 }}/> : ''
                    }
                </Col>
            </Container>
        );
    }
}

export default App;
