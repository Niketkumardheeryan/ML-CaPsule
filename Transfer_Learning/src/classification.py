import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import (models,transforms)
import copy
from tqdm import tqdm
import PIL


class ClassificationModel:

    def __init__(self, path_to_pretrained_model: str = None):
        """
        Allows for training, evaluation, and prediction of ResNet Models
        params
        ---------------
        path_to_pretrained_model - string - relative path to
            pretrained model - default None
        map_location - string - device to put model on - default cpu
        num_classes - int - number of classes to put on the deheaded ResNet
        """
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        if path_to_pretrained_model:
            self.model = torch.load(path_to_pretrained_model, map_location=self.device)
        else:
            self.model = self._setup_model(num_classes=120)
        
        self.data_transforms= self._setup_transform()

    
    def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False):
        """
            Impliments transfer learning based on new data
            params
            ---------------
            dataloaders - torch DataLoader - Configured DataLoader
                for training and validation, helpful when images are flowing from folder
            num_epochs - int - number of epochs to use during training
            criterion - Loss function to assess model during training
                and evaluation - default None and CrossEntropyLoss
            optimizer - Optimizer algorithm - default Adam
            is_inception - Parameter to specify special feature to support Inception model
            returns
            ---------------
            model - trained torch model
            val_acc_history - list - history of accuracy across epochs
        """
        since = time.time()

        val_acc_history = []
        
        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'test']:
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(DEVICE)
                    labels = labels.to(DEVICE)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        # Get model outputs and calculate loss
                        # Special case for inception because in training it has an auxiliary output. In train
                        #   mode we calculate the loss by summing the final output and the auxiliary output
                        #   but in testing we only consider the final output.
                        if is_inception and phase == 'train':
                            # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                            outputs, aux_outputs = model(inputs)
                            loss1 = criterion(outputs, labels)
                            loss2 = criterion(aux_outputs, labels)
                            loss = loss1 + 0.4*loss2
                        else:
                            outputs = model(inputs)
                            loss = criterion(outputs, labels)

                        _, preds = torch.max(outputs, 1)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / len(dataloaders[phase].dataset)
                epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'test' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
                if phase == 'test':
                    val_acc_history.append(epoch_acc)

            print()

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))

        # load best model weights
        model.load_state_dict(best_model_wts)
        return model, val_acc_history
        return self.blocks(x)
    
    
    
    def evaluate(self, test_loader, criterion=None):
        """
        Feeds set of images through model and evaluates relevant metrics
        as well as batch predicts. Prints loss and accuracy
        params
        ---------------
        test_loader - torch DataLoader - Configured
            DataLoader for evaluation, helpful when images flow from directory
        model - trained torch model - Model to use during
            evaluation - default None which retrieves model from attributes
        criterion - Loss function to assess model - Default
            None which equates to CrossEntropyLoss.
        returns
        ---------------
        preds - list - List of predictions to
            use for evaluation of non-included metrics
        labels_list - list - List of labels to
            use for evaluation of non-included metrics
        """
        if not criterion:
            criterion = nn.CrossEntropyLoss()

        model = self.model
        model.eval()
        test_loss = 0
        test_acc = 0
        preds = list()
        labels_list = list()

        for inputs, labels in test_loader:
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)

            with torch.no_grad():
                outputs = self.feed_forward(model, inputs)
                loss = criterion(outputs, labels)
                _, pred = torch.max(outputs, dim=1)
                preds.append(pred.item())
                labels_list.append(labels.item())

            test_loss += loss.item() * inputs.size(0)
            correct = pred.eq(labels.data.view_as(pred))
            accuracy = torch.mean(correct.type(torch.FloatTensor))
            test_acc += accuracy.item() * inputs.size(0)

        test_loss = test_loss / len(test_loader.dataset)
        test_acc = test_acc / len(test_loader.dataset)

        print(f"Test loss: {test_loss:.4f}\nTest acc: {test_acc:.4f}")

        return preds, labels_list

    
    def predict_proba(self, img: PIL.Image.Image, k: int, index_to_class_labels: dict, show: bool = False):
        """
        Feeds single image through network and returns
        top k predicted labels and probabilities
        params
        ---------------
        img - PIL Image - Single image to feed through model
        k - int - Number of top predictions to return
        index_to_class_labels - dict - Dictionary
            to map indices to class labels
        show - bool - Whether or not to
            display the image before prediction - default False
        returns
        ---------------
        formatted_predictions - list - List of top k
        formatted predictions formatted to include a tuple of
            1. predicted label, 2. predicted probability as str
        """
        if show:
            img.show()
        test_transform =self.data_transforms['test']    
        img = test_transform(img)
        img = img.unsqueeze(0)
        img = img.to(self.device)
        self.model.eval()
        output_tensor = self.model(img)
        prob_tensor = torch.nn.Softmax(dim=1)(output_tensor)
        top_k = torch.topk(prob_tensor, k, dim=1)
        probabilites = top_k.values.detach().numpy().flatten()
        indices = top_k.indices.detach().numpy().flatten()
        formatted_predictions = []

        for pred_prob, pred_idx in zip(probabilites, indices):
            predicted_label = index_to_class_labels[pred_idx].title()
            predicted_perc = pred_prob * 100
            formatted_predictions.append(
                (predicted_label, f"{predicted_perc:.3f}%"))

        return formatted_predictions


    def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
        # Initialize these variables which will be set in this if statement. Each of these
        #   variables is model specific.
        model_ft = None
        input_size = 0

        if model_name == "resnet":
            """ Resnet18
            """
            model_ft = models.resnet18(pretrained=use_pretrained)
            num_ftrs = model_ft.fc.in_features
            model_ft.fc = nn.Linear(num_ftrs, num_classes)
            input_size = 224

        elif model_name == "alexnet":
            """ Alexnet
            """
            model_ft = models.alexnet(pretrained=use_pretrained)
            num_ftrs = model_ft.classifier[6].in_features
            model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
            input_size = 224

        elif model_name == "vgg":
            """ VGG11_bn
            """
            model_ft = models.vgg11_bn(pretrained=use_pretrained)
            num_ftrs = model_ft.classifier[6].in_features
            model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
            input_size = 224

        elif model_name == "squeezenet":
            """ Squeezenet
            """
            model_ft = models.squeezenet1_0(pretrained=use_pretrained)
            model_ft.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
            model_ft.num_classes = num_classes
            input_size = 224

        elif model_name == "densenet":
            """ Densenet
            """
            model_ft = models.densenet121(pretrained=use_pretrained)
            num_ftrs = model_ft.classifier.in_features
            model_ft.classifier = nn.Linear(num_ftrs, num_classes) 
            input_size = 224

        elif model_name == "inception":
            """ Inception v3 
            Be careful, expects (299,299) sized images and has auxiliary output
            """
            model_ft = models.inception_v3(pretrained=use_pretrained)
            # Handle the auxilary net
            num_ftrs = model_ft.AuxLogits.fc.in_features
            model_ft.AuxLogits.fc = nn.Linear(num_ftrs, num_classes)
            # Handle the primary net
            num_ftrs = model_ft.fc.in_features
            model_ft.fc = nn.Linear(num_ftrs,num_classes)
            input_size = 299

        else:
            print("Invalid model name, exiting...")
            exit()
        
        return model_ft, input_size



    def _setup_model(self, num_classes=120):
        """
        Hidden function used in init if no pretrained model is specified.
        Helpful for implimenting transfer learning.
        It freezes all layers and then adds two final layers: one fully
        connected layer with RELU activation and dropout,
        and another as a final layer with number of class predictions
        as number of nodes. Also sends model to necessary device.
        params
        ---------------
        num_classes - int - Number of classes to predict
        returns
        ---------------
        model - torch model - torch model set up for transfer learning
        """
        model, input_size = initialize_model('resnet',num_classes, False, True)
        for param in model.parameters():
            param.require_grad = False
        model.to(self.device)
        return model

    
    def _setup_transform(self):
        """
        Sets up transformations needed for train data, val data, and test data.
        Uses much of the image processing from ImageNet paper and includes some
        image augmentation for training. Val and test transformers only perform
        minimum necessary processing.
        params
        ---------------
        None
        returns
        ---------------
        train_transform - torch transformer - transformer
            to use during training
        val_transform - torch transformer - transformer
            to use during validation
        test_transform - torch transformer - transformer
            to use during testing and inference
        """
        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(),
                transforms.RandomVerticalFlip(),
                transforms.RandomRotation(45),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'test': transforms.Compose([
                transforms.Resize((224, 224)),
        #         transforms.CenterCrop(input_size),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        }
        return data_transforms