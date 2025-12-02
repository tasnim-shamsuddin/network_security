from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score 

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        classification_metric_artifact = ClassificationMetricArtifact(
            f1_score=f1,
            accuracy_score=accuracy,
            precision_score=precision,
            recall_score=recall
        )
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    