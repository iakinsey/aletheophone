import { Heading, Button, Flex } from '@chakra-ui/react'
import { Link, useNavigate } from 'react-router-dom';


export default function Header() {
    const navigate = useNavigate()

    return (
        <Flex justify="space-between" align="center" bg="#252525" p={1}>
            <Heading as="h1" size="xl" color="#dedede">
                <Link to="/">Aletheophone</Link>
            </Heading>
            <Button colorScheme="gray" onClick={() => navigate("/create")}>
                Create
            </Button>
        </Flex>
    )
}