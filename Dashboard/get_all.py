import boto3
from botocore.exceptions import ClientError

def check_table_structure(table_name):
    """Verifica la estructura de la tabla en DynamoDB."""
    try:
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        response = dynamodb.describe_table(TableName=table_name)
        print("Estructura de la tabla:")
        for key in response['Table']['KeySchema']:
            print(f"  {key['AttributeName']} - {key['KeyType']}")
    except ClientError as e:
        print(f"Error al describir la tabla {table_name}: {e.response['Error']['Message']}")

def check_item_format(matricula, attendance_date, course_id):
    """Verifica que los datos generados para insertar sean correctos."""
    try:
        if not matricula or not attendance_date or not course_id:
            raise ValueError("Uno o más campos requeridos están vacíos (matricula, attendance_date, course_id).")

        matricula = int(matricula)
        attendance_date_course_id = f"{matricula}_{attendance_date}_{course_id}"

        # Imprime los valores generados para confirmar que todo esté bien
        print("Valores generados para la inserción:")
        print(f"Matricula: {matricula}")
        print(f"Attendance Date: {attendance_date}")
        print(f"Course ID: {course_id}")
        print(f"Generated attendance_date_course_id: {attendance_date_course_id}")

        item = {
            'attendance_date_course_id': {'S': attendance_date_course_id},
            'matricula': {'N': str(matricula)},
            'attendance_date': {'S': attendance_date},
            'attendance_time': {'S': '12:34:56'},  # Ejemplo de tiempo de asistencia
            'attendance_status': {'S': 'Present'},  # Ejemplo de estado
            'course_id': {'S': course_id}
        }
        print("Formato del Item a insertar:")
        print(item)

        return item
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

def insert_test_item(table_name, item):
    """Intenta insertar un Item en la tabla de DynamoDB."""
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        print("Respuesta de inserción:")
        print(response)
    except ClientError as e:
        print(f"Error al insertar el Item en la tabla {table_name}: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Error inesperado al insertar el Item: {str(e)}")

# Nombre de la tabla
table_name = 'Attendance'

# Verifica la estructura de la tabla
check_table_structure(table_name)

# Crea un Item de prueba y verifica que esté bien formateado
item = check_item_format(matricula=2009048, attendance_date='2024-11-03', course_id='DE2024')

# Inserta el Item de prueba si todo está correcto
if item:
    insert_test_item(table_name, item)
